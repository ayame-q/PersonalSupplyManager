<template>
	<div>
		<vue-json-csv v-bind:data="data" v-bind:labels="labels">
			<button type="button">ダウンロード</button>
		</vue-json-csv>
		<table>
			<tr>
				<th>番号</th><th>UUID</th>
			</tr>
			<tr v-for="supply in data">
				<td>{{ supply.fullNumber }}</td>
				<td>{{ supply.uuid }}</td>
			</tr>
		</table>
	</div>
</template>

<script>
import VueJsonCsv from "vue-json-csv"
export default {
	name: "SupplyCreateDownload",
	props: {
		supplies: Array
	},
	computed: {
		data() {
			let result = []
			for (const supply of this.supplies) {
				result.push({
					fullNumber: supply.type + String(supply.number).padStart(5, "0"),
					uuid: supply.uuid,
				})
			}
			return result
		}
	},
	data() {
		return {
			labels: {
				fullNumber: "番号",
				uuid: "UUID"
			}
		}
	},
	components: {
		VueJsonCsv
	}
};
</script>

<style scoped>

</style>