// 工作台 - 仪表盘
const app = getApp();

Page({
  data: {
    userInfo: {},
    userRole: '',
    userCount: 0,
    taskCount: 0,
    doingCount: 0,
  },

  onShow() {
    const info = app.globalData.userInfo;
    if (!info) {
      wx.redirectTo({ url: '/pages/login/login' });
      return;
    }
    this.setData({
      userInfo: info,
      userRole: app.globalData.userRole
    });
    this.loadStats();
  },

  loadStats() {
    // 并行请求统计数据
    Promise.all([
      app.request({ url: '/api/users' }),
      app.request({ url: '/api/tasks' })
    ]).then(([usersRes, tasksRes]) => {
      const tasks = tasksRes.tasks || [];
      this.setData({
        userCount: (usersRes.users || []).length,
        taskCount: tasks.length,
        doingCount: tasks.filter(t => t.status === 'in_progress').length
      });
    }).catch(() => {
      wx.showToast({ title: '数据加载失败', icon: 'none' });
    });
  },

  goAdminUsers() {
    wx.switchTab({ url: '/pages/admin-users/admin-users' });
  },
  goAdminTasks() {
    wx.switchTab({ url: '/pages/admin-tasks/admin-tasks' });
  },
  goMyData() {
    wx.navigateTo({ url: '/pages/my-data/my-data' });
  },
  refreshData() {
    wx.showLoading({ title: '刷新中...' });
    this.loadStats();
    setTimeout(() => wx.hideLoading(), 500);
  }
});
