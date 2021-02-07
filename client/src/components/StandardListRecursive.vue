<template>
	<div class="standard-list-recursive">
		<a v-on:click="openEdit(standard.pk)">{{ standard.name }}</a>
		<button v-on:click="deleteStandard(standard.pk, standard.name)">削除</button>
		<ul v-if="standard.children">
			<li v-for="standard in standard.children">
				<standard-list-recursive v-bind:standard="standard"></standard-list-recursive>
			</li>
		</ul>
	</div>
</template>

<script>
import StandardEdit from "@/components/StandardEdit";
export default {
	name: "StandardListRecursive",
	props: {
		standard: Object,
		isInModal: {
			type: Boolean,
			default: false
		}
	},
	components: {
		StandardEdit
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
		},
		deleteStandard(id, name) {
			this.$modal.show("dialog", {
				title: "確認",
				text: `${name}(${id})を削除しますか？`,
				buttons: [
					{
						title: "キャンセル",
						handler: () => {
							this.$modal.hide('dialog')
						}
					},
					{
						title: '削除',
						handler: () => {
							this.$api.delete(`standard/${id}`)
								.then((response) => {
									this.$store.dispatch("updateStandards")
									this.$modal.hide('dialog')
								})
						}
					},
				]
			})
		}
	}
};
</script>

<style scoped>
template, .standard-list-recursive{
	display: inline;
}
a{
	cursor: pointer;
}
</style>