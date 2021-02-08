<template>
	<div>
		<vue-json-csv v-bind:data="data" v-bind:labels="labels">
			<button type="button">ダウンロード</button>
		</vue-json-csv>
		<table>
			<tr>
				<th>番号</th><th>URL</th>
			</tr>
			<tr v-for="supply in data">
				<td>{{ supply.fullNumber }}</td>
				<td>{{ supply.url }}</td>
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
			const hostname = process.env.VUE_APP_QR_HOSTNAME
			let result = []
			for (const supply of this.supplies) {
				result.push({
					fullNumber: supply.type + String(supply.number).padStart(5, "0"),
					url: "http://" + hostname + "/" + supply.uuid.replaceAll("-", ""),
				})
			}
			return result
		}
	},
	data() {
		return {
			labels: {
				fullNumber: "番号",
				url: "URL"
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