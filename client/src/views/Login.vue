<template>
	<div class="login">
		<h2>ログイン</h2>
		<form @submit.prevent="submit">
			<dl>
				<dt><label for="username">ユーザーID</label></dt>
				<dd><input type="text" id="username" v-model="username"></dd>
				<dt><label for="password">パスワード</label></dt>
				<dd><input type="password" id="password" v-model="password"></dd>
			</dl>
			<p><input type="submit" value="ログイン"></p>
		</form>
	</div>
</template>

<script>
export default {
	name: "Login",
	data() {
		return {
			username: null,
			password: null
		}
	},
	methods: {
		submit() {
			this.$api.post("token/", {
				username: this.username,
				password: this.password
			})
			.then((response) => {
				localStorage.setItem("access", response.data.access)
				localStorage.setItem("refresh", response.data.refresh)
				console.log("Logged in")
				const next = (this.$route.query.next && !this.$route.query.next.includes("login")) ? this.$route.query.next : "/"
				this.$router.push(next)
			})
		}
	}
};
</script>

<style scoped lang="scss">

</style>