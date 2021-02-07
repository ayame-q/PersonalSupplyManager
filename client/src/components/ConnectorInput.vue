<template>
	<div class="connector-input">
		<select v-model="connector">
			<option v-for="connector in $store.getters.getConnectors" v-bind:value="connector.pk">{{ connector.name }}</option>
		</select>
		<select v-model="gender" v-if="connector">
			<option v-for="gender in $store.getters.getConnectorGenders" v-bind:value="gender.value">{{ gender.name }}</option>
		</select>
		<span v-if="connector && gender">
			<input type="number" v-model="count" >個
		</span>
	</div>
</template>

<script>
export default {
	name: "ConnectorInput",
	props: {
		id: String,
		name: String,
		value: Object, // {connector: コネクタpk, gender: コネクタの性別, count: 個数}
	},
	computed: {
		connector: {
			get() {
				return this.value.connector
			},
			set(value) {
				const data = {
					connector: value,
					gender: this.value.gender,
					count: this.value.count,
				}
				this.$emit("input", data)
			}
		},
		gender: {
			get() {
				return this.value.gender
			},
			set(value) {
				const data = {
					connector: this.value.connector,
					gender: value,
					count: this.value.count ? this.value.count : 1,
				}
				this.$emit("input", data)
			}
		},
		count: {
			get() {
				return this.value.count
			},
			set(value) {
				const data = {
					connector: this.value.connector,
					gender: this.value.gender,
					count: value,
				}
				this.$emit("input", data)
			}
		},
	},
};
</script>

<style scoped>
template, .connector-input{
	display: inline;
}
</style>