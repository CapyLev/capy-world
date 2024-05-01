import api from "../http";

export default class AuthService {
  static async login(username, password) {
    return api.post('/api/account/token/', {username, password})
  }

  static async registration(username, email, password) {
    return api.post('/api/account/register/', {username, email, password})
  }

  static async verify(token) {
    return api.post('/api/account/token/verify/', {token})
  }

  static async refresh(refresh) {
    return api.post('/api/account/token/refresh/', {refresh})
  }
}