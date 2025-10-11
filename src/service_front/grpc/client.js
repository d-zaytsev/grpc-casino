// Импорт сгенерированных gRPC-web классов
import { UserLogInfo } from './user_profile_pb';
import { UserProfileClient } from './user_profile_grpc_web_pb';

// Создаём клиента
const client = new UserProfileClient('http://localhost:8080');

/**
 * Авторизация пользователя
 * @param {string} name
 * @param {string} passwordHash
 * @param {function} callback — вызывается с (error, response)
 */
export function getUserProfile(name, passwordHash, callback) {
  const req = new UserLogInfo();
  req.setName(name);
  req.setPasswordHash(passwordHash);

  client.get_user_profile(req, {}, (err, resp) => {
    if (err) {
      callback(err, null);
      return;
    }

    const statusCode = resp.getCode();
    if (statusCode != null && statusCode != 0) {
      const new_err = {
        message: resp.getMessage() || 'Unknown server error',
        code: statusCode,
      };
      callback(new_err, null);
    } else {
      callback(null, resp);
    }

  });
}

/**
 * Регистрация нового пользователя
 * @param {string} name
 * @param {string} passwordHash
 * @param {function} callback — вызывается с (error, response)
 */
export function registerUser(name, passwordHash, callback) {
  const req = new UserLogInfo();
  req.setName(name);
  req.setPasswordHash(passwordHash);

  client.register_user(req, {}, (err, resp) => {
    if (err) {
      callback(err, null);
      return;
    }

    const statusCode = resp.getCode();
    if (statusCode != null && statusCode != 0) {
      const new_err = {
        message: resp.getMessage() || 'Unknown server error',
        code: statusCode,
      };
      callback(new_err, null);
    } else {
      callback(null, resp);
    }
  });
}
