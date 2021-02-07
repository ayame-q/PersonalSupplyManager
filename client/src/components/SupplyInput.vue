<template>
	<div class="supply-input" v-bind:id="id" >
		<input type="hidden" v-bind:name="name" v-model="localValue" disabled>
		<input type="text" v-model="supplyTitle" disabled>
		<input type="button" value="設定" v-on:click="isSearching = true">
		<input v-if="hasDeleteButton" type="button" value="削除" v-on:click="localValue = ''">
		<supply-search
			v-model="localValue"
			v-on:input="isSearching = false"
			v-bind:is-searching="isSearching"
			v-bind:supply-reject-list="supplyRejectList"
			v-on:close="isSearching = false"
		></supply-search>
	</div>
</template>

<script>
import SupplySearch from "@/components/SupplySearch";
import axios from "axios";

export default {
	name: "SupplyInput",
	components: {
		SupplySearch
	},
	props: {
		id: String,
		name: String,
		value: String,
		supplyRejectList: {
			type: Array,
			default() {
				return []
			}
		},
		hasDeleteButton: {
			type: Boolean,
			default: true
		}
	},
	data() {
		return {
			isSearching: false,
		}
	},
	computed: {
		localValue: {
			get() {
				return this.value
			},
			set(value) {
				this.$emit("input", value)
			}
		}
	},
	asyncComputed: {
		supplyTitle() {
			if (this.value) {
				axios.get(`/api/supply/${this.value}`)
					.then((response) => {
						this.supplyTitle = `${response.data.type + String(response.data.number).padStart(5, "0")}(${response.data.name})`
					})
			}
		}
	},
	methods: {
		setUUID() {
			this.isSetting = true
		},
	},
};
</script>

<style scoped lang="scss">
template, .supply-input{
	display: inline;
}
</style>