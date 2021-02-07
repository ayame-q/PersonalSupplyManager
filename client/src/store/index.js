import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    users: [],
    standards: [],
    connectors: [],
    connector_genders: [
      {name: "未定義", value: "None"},
      {name: "オス", value: "Male"},
      {name: "メス", value: "Female"}
    ],
  },
  getters: {
    getUsers(state) {
      return state.users
    },
    getStandards(state) {
      return state.standards
    },
    getTopStandards(state) {
      return state.standards.filter((standard) => {
        return standard.parent === null
      })
    },
    getConnectors(state) {
      return state.connectors
    },
    getConnectorGenders(state) {
      return state.connector_genders
    }
  },
  mutations: {
    setUsers(state, list) {
      state.users = list
    },
    clearStandards(state) {
      state.standards = []
    },
    pushStandard(state, obj) {
      state.standards.push(obj)
    },
    setConnectors(state, list) {
      state.connectors = list
    }
  },
  actions: {
    updateUsers(context) {
      Vue.prototype.$api.get(`user/`)
        .then((result) => {
          context.commit("setUsers", result.data)
        })
    },
    addStandards(context, {obj, prefix=""}) {
      obj.prefix = prefix
      context.commit("pushStandard", obj)
      for (const standard of obj.children) {
        context.dispatch("addStandards", {obj: standard, prefix: prefix + "- "})
      }
    },
    setStandards(context, list) {
      context.commit("clearStandards")
      for (const standard of list){
        context.dispatch("addStandards", {obj: standard})
      }
    },
    updateStandards(context) {
      Vue.prototype.$api.get(`standard/`)
        .then((result) => {
          context.dispatch("setStandards", result.data)
        })
    },
    updateConnectors(context) {
      Vue.prototype.$api.get(`connector/`)
        .then((result) => {
          context.commit("setConnectors", result.data)
        })
    }
  },
  modules: {
  }
})
