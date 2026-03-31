import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    sidebarCollapsed: false
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    TOGGLE_SIDEBAR(state) {
      state.sidebarCollapsed = !state.sidebarCollapsed
    },
    LOGOUT(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
    }
  },
  actions: {
    login({ commit }, { user, token }) {
      commit('SET_USER', user)
      commit('SET_TOKEN', token)
    },
    logout({ commit }) {
      commit('LOGOUT')
    },
    toggleSidebar({ commit }) {
      commit('TOGGLE_SIDEBAR')
    }
  },
  modules: {
  }
})
