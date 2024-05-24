import {auth_api} from "../http";

export default class AuthService {
  static async login(username, password) {
    return auth_api.post('/api/account/token/', {username, password});
  }

  static async registration(username, email, password) {
    return auth_api.post('/api/account/register/', {username, email, password}, {withCredentials: true})
  }

  static async verify(token) {
    return auth_api.post('/api/account/token/verify/', {token}, {withCredentials: true});
  }

  static async refresh(refresh) {
    return auth_api.post('/api/account/token/refresh/', {refresh})
  }
}