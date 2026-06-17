// 登录页
const app = getApp();

Page({
  data: {
    activeTab: 'admin',   // 'admin' | 'scan'
    adminUser: '',
    adminPwd: '',
    qrToken: ''
  },

  onLoad(options) {
    if (options.token) {
      this.setData({ activeTab: 'scan', qrToken: options.token });
      this.userLogin(options.token);
    }
  },

  switchTab(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab });
  },

  onAdminUser(e) { this.setData({ adminUser: e.detail.value }); },
  onAdminPwd(e)  { this.setData({ adminPwd: e.detail.value }); },
  onTokenInput(e){ this.setData({ qrToken: e.detail.value }); },

  adminLogin() {
    const { adminUser, adminPwd } = this.data;
    if (!adminUser || !adminPwd) {
      wx.showToast({ title: '请输入用户名和密码', icon: 'none' });
      return;
    }
    wx.showLoading({ title: '登录中...' });
    wx.request({
      url: `${app.globalData.apiBase}/api/auth/admin/login`,
      method: 'POST',
      data: { username: adminUser, password: adminPwd },
      success: (res) => {
        wx.hideLoading();
        if (res.data.success) {
          app.globalData.userInfo = res.data.admin;
          app.globalData.userRole = 'admin';
          wx.showToast({ title: '登录成功', icon: 'success' });
          setTimeout(() => wx.switchTab({ url: '/pages/dashboard/dashboard' }), 600);
        } else {
          wx.showToast({ title: '账号或密码错误', icon: 'none' });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: '无法连接服务器', icon: 'none' });
      }
    });
  },

  scanLogin() {
    const token = this.data.qrToken;
    if (!token) {
      wx.showToast({ title: '请输入二维码Token', icon: 'none' });
      return;
    }
    this.userLogin(token);
  },

  userLogin(token) {
    wx.showLoading({ title: '验证中...' });
    wx.request({
      url: `${app.globalData.apiBase}/api/auth/user/login`,
      method: 'POST',
      data: { qrcode_token: token },
      success: (res) => {
        wx.hideLoading();
        if (res.data.success) {
          app.globalData.userInfo = res.data.user;
          app.globalData.userRole = 'user';
          wx.showToast({ title: `欢迎, ${res.data.user.name}`, icon: 'success' });
          setTimeout(() => wx.navigateTo({ url: '/pages/my-data/my-data' }), 600);
        } else {
          wx.showToast({ title: '无效的二维码', icon: 'none' });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: '无法连接服务器', icon: 'none' });
      }
    });
  }
});

