const {UserLogInfo, UserProfileInfo, StatusResponse} = require('./user_profile_pb');
const {UserProfileClient } = require('./user_profile_grpc_web_pb');

const client = new UserProfileClient('http://localhost:8080');

const req = new UserLogInfo();
req.setName('arbuzka');
req.setPasswordHash('123123');

client.get_user_profile(req, {}, (err, resp) => {
  console.log(resp);
  console.log(err);
  // if (err) console.error('Error:', err);
  // else console.log(resp);
});