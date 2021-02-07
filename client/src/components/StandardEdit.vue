<template>
	<div class="standard-edit">
		<form @submit.prevent="submit">
			<dl>
				<dt><label for="name">名前</label></dt>
				<dd><input type="text" id="name" v-model="name"></dd>
				<dt><label for="parent">親規格</label></dt>
				<dd><standard-input id="parent" v-model="parent"></standard-input></dd>
			</dl>
			<p><input type="submit" value="保存"></p>
		</form>
	</div>
</template>

<script>
import axios from "axios";
import StandardInput from "@/components/StandardInput";

export default {
	name: "StandardEdit",
	props: {
		id: {
			type: Number,
			default: null
		}
	},
	data() {
		return {
			name: null,
			parent: null,
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
			httpRequest(`/api/standard/${this.id ? this.id : ""}`, {
				name: this.name,
				parent: this.parent
			})
			.then((response) => {
				this.$store.dispatch("updateStandards")
				this.$emit("close")
			})
			.catch((error) => {
				alert("Error" + error)
			})
		}
	},
	created() {
		if (this.id) {
			axios.get(`/api/standard/${this.id}`)
				.then((response) => {
					const result = response.data
					this.name = result.name
					this.parent = result.parent
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