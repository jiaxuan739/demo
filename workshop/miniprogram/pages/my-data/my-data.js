// 我的数据页
const app = getApp();

Page({
  data: {
    userInfo: {},
    tasks: [],
    doingCount: 0,
    doneCount: 0,
    statusMap: app.globalData.statusMap
  },

  onShow() {
    const user = app.globalData.userInfo;
    if (!user) {
      wx.redirectTo({ url: '/pages/login/login' });
      return;
    }
    this.setData({ userInfo: user });
    this.loadTasks(user.id);
  },

  loadTasks(userId) {
    wx.showLoading({ title: '加载中...' });
    wx.request({
      url: `${app.globalData.apiBase}/api/tasks/my/${userId}`,
      success: (res) => {
        wx.hideLoading();
        const tasks = res.data.tasks || [];
        this.setData({
          tasks,
          doingCount: tasks.filter(t => t.status === 'in_progress').length,
          doneCount: tasks.filter(t => t.status === 'completed').length
        });
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({ title: '加载失败', icon: 'none' });
      }
    });
  }
});

