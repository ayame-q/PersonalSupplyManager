<template>
	<div class="index">
		<supply-search
			v-bind:is-searching="isOpenCamera"
			v-on:input="jumpToSupplyPage"
			v-on:close="isOpenCamera=false"
			v-bind:can-close="false"
		></supply-search>
		<p class="open-camera-button"><button v-on:click="isOpenCamera = true">カメラを起動</button></p>
	</div>
</template>

<script>
import SupplySearch from "@/components/SupplySearch";

export default {
	name: "Index",
	components: {
		SupplySearch
	},
	data() {
		return {
			isOpenCamera: true,
		}
	},
	computed: {
	},
	methods: {
		jumpToSupplyPage(uuid) {
			this.$router.push(`/${uuid.replaceAll("-", "")}`)
		}
	},
};
</script>

<style scoped lang="scss">
.index{
	.open-camera-button{
		position: fixed;
		top: 50%;
		left: 50%;
		z-index: 0;
		transform: translate(-50%, -50%);
		button{
			font-size: 5vw;
		}
	}
}
</style>