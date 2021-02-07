<template>
	<div class="standard-list">
		<ul>
			<li v-for="standard in $store.getters.getTopStandards">
				<standard-list-recursive v-bind:standard="standard" v-bind:is-in-modal="isInModal"></standard-list-recursive>
			</li>
		</ul>
		<p><a v-on:click="openEdit()">追加</a></p>
		<v-dialog />
	</div>
</template>

<script>
import StandardListRecursive from "@/components/StandardListRecursive";
import StandardEdit from "@/components/StandardEdit";

export default {
	name: "StandardList",
	props: {
		isInModal: {
			type: Boolean,
			default: false
		}
	},
	components: {
		StandardListRecursive
	},
	methods: {
		openEdit(id=null) {
			this.$modal.show(
				StandardEdit,
				{id: id},
				{
					height: "auto",
					scrollable: true,
				}
			)
		}
	},
	created() {
		this.$store.dispatch("updateStandards")
	},
};
</script>

<style lang="scss" scoped>
.standard-list{
	padding: 2em;
	a{
		cursor: pointer;
	}
}
</style>