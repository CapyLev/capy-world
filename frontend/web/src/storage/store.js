import {makeAutoObservable} from "mobx";
import AuthService from "../services/AuthService";
import UserService from "../services/UserService";

export default class Store {
  user = {};
  isAuth = false;
  isLoading = false;

  constructor() {
    makeAutoObservable(this);
  }

  setAuth(status) {
    this.isAuth = status;
  }

  setUser(user) {
    this.user = user;
  }

  setLoading(status) {
    this.isLoading = status;
  }

  setDefault() {
    this.user = {};
    this.isAuth = false;
    this.isLoading = false;
  }

  async setUserInfo() {
    const user_info_response = await UserService.getUserInfo();
    this.setUser(user_info_response.data);
  }

  async login(username, password) {
    try {
      const response = await AuthService.login(username, password);
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      this.setAuth(true);
      await this.setUserInfo()
    } catch (error) {
      console.log(error)
    }
  }

  async register(username, email, password) {
    try {
      await AuthService.registration(username, email, password);

      const response = await AuthService.login(username, password);
      localStorage.setItem('access', response.data.access);
      this.setAuth(true);

      await this.setUserInfo()
    } catch (e) {
      console.log(e.response.data.message)
    }
  }

  // TODO: delete?
  async checkAuth() {
    try {
      this.setLoading(true)
      const access = localStorage.getItem('access');

      if (!access) {
        this.setDefault()
        return
      }

      const response = await AuthService.verify(access);
      if (response.status === 200) {
        await this.setUserInfo()
        this.setAuth(true)
      }
    } catch (error) {
      this.setDefault();
    }
  }
}
