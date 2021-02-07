<template>
	<div class="standard-list">
		<ul>
			<li v-for="connector in $store.getters.getConnectors">
				<a v-on:click="openEdit(connector.pk)">{{ connector.name }}</a>
				<button v-on:click="deleteConnector(connector.pk, connector.name)">削除</button>
			</li>
		</ul>
		<p><a v-on:click="openEdit()">追加</a></p>
		<v-dialog />
	</div>
</template>

<script>
import ConnectorEdit from "@/components/ConnectorEdit";

export default {
	name: "ConnectorList",
	props: {
		isInModal: {
			type: Boolean,
			default: false
		}
	},
	methods: {
		openEdit(id=null) {
			this.$modal.show(
				ConnectorEdit,
				{id: id},
				{
					height: "auto",
					scrollable: true,
				}
			)
		},
		deleteConnector(id, name) {
			this.$modal.show('dialog', {
				title: "確認",
				text: `${name}を削除しますか？`,
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
							this.$api.delete(`connector/${id}`)
								.then((response) => {
									this.$store.dispatch("updateConnectors")
									this.$modal.hide('dialog')
								})
						}
					},
				]
			})
		}
	},
	created() {
		this.$store.dispatch("updateConnectors")
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