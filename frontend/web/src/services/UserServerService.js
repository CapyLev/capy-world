import api from "../http";

export default class UserServerService {
  static async fetchUserServers() {
    return api.get('/'); // TODO:
  }
}