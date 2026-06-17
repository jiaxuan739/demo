// 管理员 - 人员管理
const app = getApp();

Page({
  data: {
    users: [],
    showModal: false,
    editId: null,
    form: { student_id: '', name: '', class_name: '', phone: '' }
  },

  onShow() { this.loadUsers(); },

  loadUsers() {
    wx.request({
      url: `${app.globalData.apiBase}/api/users`,
      success: (res) => this.setData({ users: res.data.users }),
      fail: () => wx.showToast({ title: '加载失败', icon: 'none' })
    });
  },

  showAdd() {
    this.setData({ showModal: true, editId: null, form: { student_id: '', name: '', class_name: '', phone: '' } });
  },

  editUser(e) {
    const { id, name, class: cls } = e.currentTarget.dataset;
    const user = this.data.users.find(u => u.id === id);
    this.setData({ showModal: true, editId: id, form: { ...user } });
  },

  closeModal() { this.setData({ showModal: false }); },

  onField(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({ [`form.${field}`]: e.detail.value });
  },

  submitUser() {
    const { editId, form } = this.data;
    const url = editId
      ? `${app.globalData.apiBase}/api/users/${editId}`
      : `${app.globalData.apiBase}/api/users`;
    const method = editId ? 'PUT' : 'POST';

    wx.request({
      url, method,
      data: editId ? { name: form.name, class_name: form.class_name, phone: form.phone } : form,
      success: (res) => {
        if (res.data.success) {
          wx.showToast({ title: editId ? '已更新' : '已添加', icon: 'success' });
          this.setData({ showModal: false });
          this.loadUsers();
        }
      },
      fail: () => wx.showToast({ title: '失败', icon: 'none' })
    });
  },

  deleteUser(e) {
    const { id, name } = e.currentTarget.dataset;
    wx.showModal({
      title: '确认删除',
      content: `确定删除 ${name} 吗？`,
      success: (res) => {
        if (res.confirm) {
          wx.request({
            url: `${app.globalData.apiBase}/api/users/${id}`,
            method: 'DELETE',
            success: () => { wx.showToast({ title: '已删除', icon: 'success' }); this.loadUsers(); }
          });
        }
      }
    });
  }
});
