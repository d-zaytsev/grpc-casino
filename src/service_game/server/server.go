package main

import (
	"context"
	"log"
	"math/rand"
	"net"
	"time"

	slotpb "github.com/d-zaytsev/grpc-casino/gen/go/service_game/protos"
	balancepb "github.com/d-zaytsev/grpc-casino/gen/go/user_balance/protos"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"
	"google.golang.org/grpc/reflection"
)

const (
	// Money constants
	SPIN_COST = 100.0
	PAYOUT    = 200.0

	// Behaviour tuning
	spinFrames      = 8
	frameDelay      = 120 * time.Millisecond
	numSymbols      = 8 // symbol ids are 0..7
	withdrawTimeout = 800 * time.Millisecond
	depositTimeout  = 1 * time.Second
)

type gameServer struct {
	slotpb.UnimplementedGameServiceServer
	balanceClient balancepb.UserBalanceClient
}

func newGameServer(balanceAddr string) (*gameServer, error) {
	conn, err := grpc.Dial(balanceAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}
	client := balancepb.NewUserBalanceClient(conn)
	return &gameServer{balanceClient: client}, nil
}

func (s *gameServer) withdraw(ctx context.Context, userUUID string, amount float64) error {
	ctx2, cancel := context.WithTimeout(ctx, withdrawTimeout)
	defer cancel()

	req := &balancepb.UpdateRequest{
		UserUuid:    userUUID,
		AmountDelta: amount,
	}
	resp, err := s.balanceClient.Withdraw(ctx2, req)
	if err != nil {
		return err
	}
	if resp.Code != 0 {
		return status.Errorf(codes.PermissionDenied, "withdraw failed: %s", resp.Message)
	}
	return nil
}

func (s *gameServer) deposit(ctx context.Context, userUUID string, amount float64) error {
	ctx2, cancel := context.WithTimeout(ctx, depositTimeout)
	defer cancel()

	req := &balancepb.UpdateRequest{
		UserUuid:    userUUID,
		AmountDelta: amount,
	}
	resp, err := s.balanceClient.Deposit(ctx2, req)
	if err != nil {
		return err
	}
	if resp.Code != 0 {
		return status.Errorf(codes.Internal, "deposit failed: %s", resp.Message)
	}
	return nil
}

func randomRow() []int32 {
	return []int32{
		int32(rand.Intn(numSymbols)),
		int32(rand.Intn(numSymbols)),
		int32(rand.Intn(numSymbols)),
	}
}

func isWin(row []int32) bool {
	return len(row) == 3 && row[0] == row[1] && row[1] == row[2]
}

func (s *gameServer) GetResults(req *slotpb.SpinRequest, stream slotpb.GameService_GetResultsServer) error {
	ctx := stream.Context()
	user := req.UserUuid
	if user == "" {
		_ = stream.Send(&slotpb.SpinResult{Symbols: nil, IsFinal: true})
		return status.Error(codes.InvalidArgument, "user_uuid required")
	}

	if err := s.withdraw(ctx, user, SPIN_COST); err != nil {
		log.Printf("withdraw failed for user=%s: %v", user, err)
		_ = stream.Send(&slotpb.SpinResult{Symbols: nil, IsFinal: true})
		return err
	}

	cancelled := false
	for i := 0; i < spinFrames; i++ {
		row := randomRow()
		if err := stream.Send(&slotpb.SpinResult{Symbols: row, IsFinal: false}); err != nil {
			log.Printf("failed to send frame to user=%s: %v", user, err)
			// stop trying to send more frames; still proceed to compute/settle
			cancelled = true
			break
		}

		select {
		case <-time.After(frameDelay):
			// continue to next frame
		case <-ctx.Done():
			log.Printf("client cancelled for user=%s: %v", user, ctx.Err())
			cancelled = true
			break
		}
		if cancelled {
			break
		}
	}

	final := randomRow()
	win := isWin(final)

	if win {
		if err := s.deposit(context.Background(), user, PAYOUT); err != nil {
			// deposit failed — log and still try to inform client with final frame (if connected).
			log.Printf("deposit failed for user=%s payout=%.2f: %v", user, PAYOUT, err)
			_ = stream.Send(&slotpb.SpinResult{Symbols: final, IsFinal: true})
			return status.Error(codes.Internal, "deposit failed")
		}
	}

	if err := stream.Send(&slotpb.SpinResult{Symbols: final, IsFinal: true}); err != nil {
		log.Printf("failed to send final frame to user=%s: %v", user, err)
		return err
	}

	return nil
}

func main() {
	const balanceAddr = "127.0.0.1:5005"
	srv, err := newGameServer(balanceAddr)
	if err != nil {
		log.Fatalf("failed to create game server: %v", err)
	}

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("listen failed: %v", err)
	}

	grpcServer := grpc.NewServer()
	slotpb.RegisterGameServiceServer(grpcServer, srv)
	reflection.Register(grpcServer)

	log.Println("game service listening on :50051")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("serve failed: %v", err)
	}
}
