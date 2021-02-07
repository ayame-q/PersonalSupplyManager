<template>
	<div class="supply-search-result-list">
		<p v-if="message">{{ message }}</p>
		<table>
			<tr>
				<th>番号</th><th>種類</th><th>名前</th><th>メーカー</th><th>設置場所</th>
			</tr>
			<tr v-for="supply in supplies" v-on:click="localValue = supply.uuid">
				<td>
					{{ supply.type + String(supply.number).padStart(5, "0") }}
				</td>
				<td>
					{{ supply.category }}
				</td>
				<td>
					{{ supply.name }}
				</td>
				<td>
					{{ supply.manufacturer }}
				</td>
				<td>
					{{ supply.position }}
				</td>
			</tr>
		</table>
	</div>
</template>

<script>
export default {
	name: "SupplySearchResultList",
	props: {
		supplies: Array,
		value: String,
		message: String,
	},
	computed: {
		localValue: {
			get() {
				return this.value
			},
			set(value) {
				this.$emit("close", value)
			}
		}
	},
};
</script>

<style scoped>
.supply-search-result-list{
	padding: 2em;
	width: fit-content;
}
</style>