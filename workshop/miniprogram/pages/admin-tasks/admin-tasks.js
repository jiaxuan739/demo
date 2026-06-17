// 管理员 - 任务管理
const app = getApp();

Page({
  data: {
    tasks: [],
    filteredTasks: [],
    activeFilter: 'all',
    showModal: false,
    editId: null,
    statusOptions: ['pending', 'in_progress', 'completed'],
    statusLabels: ['⏳ 待处理', '🔄 进行中', '✅ 已完成'],
    statusIndex: 0,
    statusMap: app.globalData.statusMap,
    form: { user_id: '', title: '', description: '', status: 'pending', quantity: 0, deadline: '' }
  },

  onShow() { this.loadTasks(); },

  loadTasks() {
    wx.showLoading({ title: '加载中...' });
    wx.request({
      url: `${app.globalData.apiBase}/api/tasks`,
      success: (res) => {
        wx.hideLoading();
        const tasks = res.data.tasks || [];
        this.setData({ tasks });
        this.applyFilter(this.data.activeFilter);
      },
      fail: () => { wx.hideLoading(); wx.showToast({ title: '加载失败', icon: 'none' }); }
    });
  },

  setFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({ activeFilter: filter });
    this.applyFilter(filter);
  },

  applyFilter(filter) {
    const tasks = filter === 'all'
      ? this.data.tasks
      : this.data.tasks.filter(t => t.status === filter);
    this.setData({ filteredTasks: tasks });
  },

  showAdd() {
    this.setData({
      showModal: true, editId: null, statusIndex: 0,
      form: { user_id: '', title: '', description: '', status: 'pending', quantity: 0, deadline: '' }
    });
  },

  editTask(e) {
    const { id } = e.currentTarget.dataset;
    const task = this.data.tasks.find(t => t.id === id);
    const si = this.data.statusOptions.indexOf(task.status);
    this.setData({ showModal: true, editId: id, statusIndex: si >= 0 ? si : 0, form: { ...task } });
  },

  closeModal() { this.setData({ showModal: false }); },

  onField(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({ [`form.${field}`]: e.detail.value });
  },

  onStatusChange(e) {
    const idx = parseInt(e.detail.value);
    this.setData({ statusIndex: idx, 'form.status': this.data.statusOptions[idx] });
  },

  submitTask() {
    const { editId, form } = this.data;
    if (!form.title || !form.user_id) {
      wx.showToast({ title: '请填写标题和负责人', icon: 'none' });
      return;
    }
    const url = editId
      ? `${app.globalData.apiBase}/api/tasks/${editId}`
      : `${app.globalData.apiBase}/api/tasks`;
    const method = editId ? 'PUT' : 'POST';

    wx.showLoading({ title: '保存中...' });
    wx.request({
      url, method, data: form,
      success: (res) => {
        wx.hideLoading();
        if (res.data.success) {
          wx.showToast({ title: editId ? '已更新' : '已创建', icon: 'success' });
          this.setData({ showModal: false });
          this.loadTasks();
        }
      },
      fail: () => { wx.hideLoading(); wx.showToast({ title: '保存失败', icon: 'none' }); }
    });
  },

  deleteTask(e) {
    const { id, title } = e.currentTarget.dataset;
    wx.showModal({
      title: '确认删除',
      content: `确定删除「${title}」吗？`,
      confirmColor: '#FF3B30',
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: `${app.globalData.apiBase}/api/tasks/${id}`,
            method: 'DELETE',
            success: () => {
              wx.showToast({ title: '已删除', icon: 'success' });
              this.loadTasks();
            }
          });
        }
      }
    });
  }
});

