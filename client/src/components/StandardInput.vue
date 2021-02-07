<template>
	<select v-bind:id="id" v-model="localValue">
		<option v-for="standard in $store.getters.getStandards" v-bind:value="standard.pk">{{ standard.prefix }}{{ standard.name }}</option>
	</select>
</template>

<script>
export default {
	name: "StandardInput",
	props: {
		id: String,
		name: String,
		value: Number,
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
};
</script>

<style scoped lang="scss">
template{
	display: inline;
}
</style>