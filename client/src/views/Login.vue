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
		<v-dialog />
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
					this.jumpToNext()
				})
				.catch((error) => {
					const error_message = error.response.status === 401 ? "ユーザーIDかパスワードが間違っています" : `不明なエラーが発生しました(${error.response.status})`
					this.$modal.show('dialog', {
						title: "エラー",
						text: "ユーザーIDかパスワードが間違っています",
						buttons: [
							{
								title: '閉じる',
								handler: () => {
									this.$modal.hide('dialog')
								}
							},
						]
					})
				})
		},
		jumpToNext() {
			const next = (this.$route.query.next && !this.$route.query.next.includes("login")) ? this.$route.query.next : "/"
			this.$router.push(next)
		}
	},
	created() {
		const refreshToken = localStorage.getItem("refresh")
		if (refreshToken) {
			this.$api.post("token/verify/", {
				token: refreshToken
			})
				.then((result) => {
					if (result.status === 200) {
						console.log("You have logged in")
						this.jumpToNext()
					}
				})
		}
	}
};
</script>

<style scoped lang="scss">

</style>