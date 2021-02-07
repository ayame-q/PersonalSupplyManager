<template>
	<div class="supply-create-page">
		<form @submit.prevent="submit">
			<dl>
				<dt><label for="type">名前</label></dt>
				<dd>
					<select id="type" v-model="type">
						<option v-for="type in $store.getters.getSupplyTypes" v-bind:value="type.value">{{ type.name }}</option>
					</select>
				</dd>
				<dt><label for="count">数</label></dt>
				<dd><input type="number" id="count" v-model="count"></dd>
			</dl>
			<p><input type="submit" value="作成"></p>
		</form>
	</div>
</template>

<script>
import SupplyCreateDownload from "@/components/SupplyCreateDownload";

export default {
	name: "SupplyCreatePage",
	data() {
		return {
			type: null,
			count: null
		}
	},
	methods: {
		submit() {
			this.$api.post("supply/create", {
				type: this.type,
				count: this.count
			})
			.then((response) => {
				this.$modal.show(
					SupplyCreateDownload,
					{supplies: response.data},
					{
						height: "auto",
						scrollable: true,
					}
				)
			})
		}
	}
};
</script>

<style scoped>

</style>