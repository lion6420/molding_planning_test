import axios from 'axios'

export default {
  //Planning result
  get_result () {
    return axios.request({
      baseURL: 'http://localhost:5000/',
      url: 'planningresult',
      method: 'get',
    })
  },

  // Emergency
  get_emergency () {
    return axios.request({
      baseURL: 'http://localhost:5000/',
      url: 'emergency',
      method: 'get',
    })
  },
  update_emergency (data) {
    return axios.request({
      baseURL: 'http://localhost:5000/',
      url: 'emergency/adjust',
      method: 'post',
      data: data,
    })
  },
  delete_all () {
    return axios.request({
      baseURL: 'http://localhost:5000/',
      url: 'emergency/adjust',
      method: 'delete',
    })
  },
  get_weeklydemand(page, size) {
    return axios.request({
      baseURL: 'http://localhost:5000/',
      url: 'weekly',
      method: 'post',
      data: {page:page, size:size}
    })
  },
  update_weeklydemand() {
    return axios.request({
      baseURL: 'http://localhost:5000/',
      url: 'weekly',
      method: 'put',
    })
  }
}