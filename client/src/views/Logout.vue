<template>
	<div class="logout">
		<p>ログアウトしています...</p>
	</div>
</template>

<script>
export default {
	name: "Logout",
	created() {
		localStorage.removeItem("access")
		localStorage.removeItem("refresh")
		const next = (this.$route.query.next && !this.$route.query.next.includes("logout")) ? this.$route.query.next : "/"
		this.$router.push(next)
	}
};
</script>

<style scoped lang="scss">

</style>