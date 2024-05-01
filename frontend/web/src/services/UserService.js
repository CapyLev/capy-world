import api from "../http";

export default class UserService {
  static async getUserInfo() {
    return api.get('/api/account/user');
  }
}