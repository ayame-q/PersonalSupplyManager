<template>
	<div class="standard-edit">
		<h2>コネクタを<span v-if="id">編集</span><span v-else>追加</span></h2>
		<form @submit.prevent="submit">
			<dl>
				<dt><label for="name">名前</label></dt>
				<dd><input type="text" id="name" v-model="name"></dd>
				<dt><label for="standard">規格</label></dt>
				<dd><standard-input id="standard" v-model="standard"></standard-input></dd>
			</dl>
			<p><input type="submit" value="保存"></p>
		</form>
	</div>
</template>

<script>
import axios from "axios";
import StandardInput from "@/components/StandardInput";

export default {
	name: "ConnectorEdit",
	props: {
		id: {
			type: Number,
			default: null
		}
	},
	data() {
		return {
			name: null,
			standard: null,
		}
	},
	components: {
		StandardInput
	},
	methods: {
		submit(event) {
			axios.defaults.xsrfCookieName = 'csrftoken'
			axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
			const httpRequest = this.id ? axios.put : axios.post
			httpRequest(`/api/connector/${this.id ? this.id : ""}`, {
				name: this.name,
				standard: this.standard
			})
			.then((response) => {
				this.$store.dispatch("updateConnectors")
				this.$emit("close")
			})
			.catch((error) => {
				alert("Error" + error)
			})
		}
	},
	created() {
		if (this.id) {
			axios.get(`/api/connector/${this.id}`)
				.then((response) => {
					const result = response.data
					this.name = result.name
					this.standard = result.standard
				})
		}
	}
};
</script>

<style scoped>
.standard-edit{
	padding: 2em;
}
</style>