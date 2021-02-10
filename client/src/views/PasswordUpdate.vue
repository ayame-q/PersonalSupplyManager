<template>
	<div class="password_update">
		<h2>パスワードを変更</h2>
		<form @submit.prevent="submit">
			<dl>
				<dt><label for="old_password">現在のパスワード</label></dt>
				<dd><input type="password" id="old_password" v-model="old_password"></dd>
				<dt><label for="password">新しいパスワード</label></dt>
				<dd><input type="password" id="password" v-model="password"></dd>
				<dt><label for="password2">新しいパスワード(確認)</label></dt>
				<dd><input type="password" id="password2" v-model="password2"></dd>
			</dl>
			<p><input type="submit" value="変更"></p>
		</form>
		<v-dialog />
	</div>
</template>

<script>
export default {
	name: "Login",
	data() {
		return {
			old_password: null,
			password: null,
			password2: null
		}
	},
	methods: {
		submit() {
			this.$api.put("account/change_password", {
				old_password: this.old_password,
				password: this.password,
				password2: this.password2
			})
				.then((response) => {
					this.$modal.show('dialog', {
						title: "",
						text: `パスワードを変更しました。`,
						buttons: [
							{
								title: 'OK',
								handler: () => {
									this.$modal.hide('dialog')
									this.$router.push("/")
								}
							},
						]
					}, {
						clickToClose: false
					})
				})
				.catch((error) => {
					console.log(error.response)
					let error_message = ""
					for (let e of Object.values(error.response.data)) {
						console.log(typeof Object())
						if (typeof e === typeof Object())
							e = Object.values(e)
						error_message += "<div>" + e.join("<br>") + "</div>"
					}
					this.$modal.show('dialog', {
						title: "エラー",
						text: error_message,
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
	},
};
</script>

<style scoped lang="scss">

</style>