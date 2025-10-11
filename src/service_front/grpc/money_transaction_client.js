import { UserDepositRequest, TransactionResponse } from './money_transcation_pb';
import { MoneyTransactonClient } from './money_transcation_grpc_web_pb';

const client = new MoneyTransactonClient('http://localhost:8081');

/**
 * Внести депозит пользователю
 * @param {string} name
 * @param {string} passwordHash
 * @param {number} amount
 * @param {function} callback — вызывается с (error, response)
 */
export function deposit(name, passwordHash, amount, callback) {
  const req = new UserDepositRequest();
  req.setName(name);
  req.setPasswordHash(passwordHash);
  req.setAmount(amount);

  client.deposit(req, {}, (err, resp) => {
    if (err) {
      callback(err, null);
      return;
    }

    const statusCode = resp.getCode();
    if (statusCode != null && statusCode !== TransactionResponse.StatusCode.OK) {
      const newErr = {
        message: resp.getMessage() || 'Unknown server error',
        code: statusCode,
      };
      callback(newErr, null);
    } else {
      callback(null, resp);
    }
  });
}

/**
 * Снять средства с пользователя
 * @param {string} name
 * @param {string} passwordHash
 * @param {number} amount
 * @param {function} callback — вызывается с (error, response)
 */
export function withdraw(name, passwordHash, amount, callback) {
  const req = new UserDepositRequest();
  req.setName(name);
  req.setPasswordHash(passwordHash);
  req.setAmount(amount);

  client.withdraw(req, {}, (err, resp) => {
    if (err) {
      callback(err, null);
      return;
    }

    const statusCode = resp.getCode();
    if (statusCode != null && statusCode !== TransactionResponse.StatusCode.OK) {
      const newErr = {
        message: resp.getMessage() || 'Unknown server error',
        code: statusCode,
      };
      callback(newErr, null);
    } else {
      callback(null, resp);
    }
  });
}
