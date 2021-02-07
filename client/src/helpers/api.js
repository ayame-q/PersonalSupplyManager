import axios from "axios";
import router from "@/router";
import Vue from "vue";

const api = axios.create({
	baseURL: process.env.VUE_APP_ROOT_API ? process.env.VUE_APP_ROOT_API : "/api/",
	timeout: 5000,
	headers: {
		"Content-Type": "application/json",
		"X-Requested-With": "XMLHttpRequest"
	}
})

api.interceptors.request.use((config) => {
	const token = localStorage.getItem("access")
	if (!token) {
		router.push("/login")
		return config
	}
	config.headers.Authorization = "Bearer " + token
	return config
}, (error) => {
	return Promise.reject(error)
})

api.interceptors.response.use((response) => {
	return response
}, (error) => {
	if (error.response.status === 401){
		const token = localStorage.getItem("access")
		if (!token){
			console.log("Jumpping to Login Page")
			router.push({
				path: "/login",
				query: {
					next: router.currentRoute.fullPath
				}
			})
			return Promise.reject(error)
		} else {
			const config = error.config

			return api.post("token/refresh/", {
				refresh: localStorage.getItem("refresh")
			})
				.then((response) => {
					localStorage.setItem("access", response.data.access)
					console.log("Token refreshed")
					return api(config)
				})
				.catch((error) => {
					router.push({
						path: "/login",
						query: {
							next: router.currentRoute.fullPath
						}
					})
					return Promise.reject(error)
				})
		}
	}
	return Promise.reject(error)
})

const apiPlugin = {
	install () {
		Vue.prototype.$api = api
	}
}

export default apiPlugin
