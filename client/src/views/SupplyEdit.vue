<template>
	<div class="supply">
		<form @submit.prevent="submit" v-if="!error">
			<dl>
				<dt><label for="uuid">UUID</label></dt>
				<dd><input type="text" id="uuid" v-model="uuid" disabled></dd>
				<dt><label for="full-number">番号</label></dt>
				<dd><input type="text" id="full-number" v-model="fullNumber" disabled></dd>
				<dt><label for="category">種類</label></dt>
				<dd><input type="text" id="category" v-model="category"></dd>
				<dt><label for="name">名前</label></dt>
				<dd><input type="text" id="name" v-model="name"></dd>
				<dt><label for="manufacturer">メーカー</label></dt>
				<dd><input type="text" id="manufacturer" v-model="manufacturer"></dd>
				<dt><label for="model">型番</label></dt>
				<dd><input type="text" id="model" v-model="model"></dd>
				<dt><label for="serial-number">シリアルナンバー</label></dt>
				<dd><input type="text" id="serial-number" v-model="serial_number"></dd>
				<dt><label for="length">長さ(cm)</label></dt>
				<dd><input type="text" id="length" v-model="length"></dd>
				<dt><label for="owner">所有者</label></dt>
				<dd>
					<select id="owner" v-model="owner" multiple>
						<option v-for="user in $store.getters.getUsers" v-bind:value="user.pk">{{ user.username }}</option>
					</select>
				</dd>
				<dt><label for="bought_at">購入日</label></dt>
				<dd><input type="date" id="bought_at" v-model="bought_at"></dd>
				<dt><label for="parent">本体</label></dt>
				<dd><supply-input id="parent" v-model="parent"></supply-input></dd>
				<dt><label for="standards">規格</label><button type="button" v-on:click="openStandardsManage">管理</button></dt>
				<dd id="standards">
					<div v-for="(standard, index) in standards">
						<standard-input v-model="standards[index]"></standard-input>
						<input type="button" v-on:click="standards.splice(index, 1)" value="削除">
					</div>
					<div>
						<input type="button" v-on:click="standards.push(null)" value="追加">
					</div>
				</dd>
				<dt><label for="connectors">コネクタ</label><button type="button" v-on:click="openConnectorsManage">管理</button></dt>
				<dd id="connectors">
					<div v-for="(connector, index) in connectors">
						<connector-input v-model="connectors[index]"></connector-input>
						<input type="button" v-on:click="connectors.splice(index, 1)" value="削除">
					</div>
					<div>
						<input type="button" v-on:click="connectors.push({})" value="追加">
					</div>
				</dd>
				<dt><label for="connected_supplies">接続先</label></dt>
				<dd id="connected_supplies">
					<div v-for="(connected_supply, index) in connected_supplies">
						<supply-input v-model="connected_supplies[index]" v-bind:has-delete-button="false" v-bind:supply-reject-list="connected_supplies"></supply-input>
						<input type="button" v-on:click="connected_supplies.splice(index, 1)" value="削除">
					</div>
					<div>
						<input type="button" v-on:click="connected_supplies.push('')" value="追加">
					</div>
				</dd>
				<dt><label for="position">設置場所</label></dt>
				<dd><input type="text" id="position" v-model="position"></dd>
			</dl>
			<p><input type="checkbox" id="is_power_cable" v-model="is_power_cable"><label for="is_power_cable">電源線か</label></p>
			<p><input type="checkbox" id="is_signal_cable" v-model="is_signal_cable"><label for="is_signal_cable">信号線か</label></p>
			<p><input type="checkbox" id="is_active_cable" v-model="is_active_cable"><label for="is_active_cable">アクティブケーブルか</label></p>
			<dl>
				<dt><label for="note">備考</label></dt>
				<dd><textarea id="note" v-model="note"></textarea></dd>
			</dl>
			<p><input type="submit" value="保存"></p>
		</form>
		<div class="error" v-else>
			<p>{{ error }}</p>
		</div>
	</div>
</template>

<script>
// @ is an alias to /src
import SupplyInput from "@/components/SupplyInput";
import ConnectorInput from "@/components/ConnectorInput";
import StandardInput from "@/components/StandardInput";
import StandardList from "@/components/StandardList";
import ConnectorList from "@/components/ConnectorList";

export default {
	name: "SupplyEdit",
	data() {
		return {
			connectorInput: ConnectorInput,
			uuid: this.$route.params.uuid,
			type: null,
			number: null,
			category: null,
			name: null,
			manufacturer: null,
			model: null,
			serial_number: null,
			length: null,
			owner: [],
			bought_at: null,
			parent: null,
			standards: [],
			connectors: [{}],
			connected_supplies: [],
			position: null,
			is_power_cable: null,
			is_signal_cable: null,
			is_active_cable: null,
			note: null,
			error: null,
		};
	},
	computed: {
		fullNumber() {
			if (!this.number) {
				return null
			}
			return this.type + String(this.number).padStart(5, "0")
		}
	},
	components: {
		SupplyInput,
		ConnectorInput,
		StandardInput,
	},
	methods: {
		submit(event) {
			this.$api.put(`supply/${this.uuid}`, {
				uuid: this.uuid,
				type: this.type,
				number: this.number,
				category: this.category,
				name: this.name,
				manufacturer: this.manufacturer,
				model: this.model,
				serial_number: this.serial_number,
				length: this.length,
				owner: this.owner,
				bought_at: this.bought_at,
				parent: this.parent,
				standards: this.standards,
				connectors: this.connectors,
				connected_supplies: this.connected_supplies,
				position: this.position,
				is_power_cable: this.is_power_cable,
				is_signal_cable: this.is_signal_cable,
				is_active_cable: this.is_active_cable,
				note: this.note,
			})
			.then(() => {
				this.$router.push("/")
			})
			.catch((error) => {
				alert("Error" + error)
			})
		},
		openStandardsManage() {
			this.$modal.show(
				StandardList,
				{},
			)
		},
		openConnectorsManage() {
			this.$modal.show(
				ConnectorList,
				{},
			)
		}
	},
	created() {
		this.$store.dispatch("updateUsers")
		this.$store.dispatch("updateStandards")
		this.$store.dispatch("updateConnectors")
		this.$api.get(`supply/${this.uuid}`)
		.then((response) => {
			const result = response.data
			this.uuid = result.uuid
			this.type = result.type
			this.number = result.number
			this.category = result.category
			this.name = result.name
			this.manufacturer = result.manufacturer
			this.model = result.model
			this.serial_number = result.serial_number
			this.length = result.length
			this.owner = result.owner
			this.bought_at = result.bought_at
			this.parent = result.parent
			this.standards = result.standards
			this.connectors = result.connectors
			this.connected_supplies = result.connected_supplies
			this.position = result.position
			this.is_power_cable = result.is_power_cable
			this.is_signal_cable = result.is_signal_cable
			this.is_active_cable = result.is_active_cable
			this.note = result.note
		})
		.catch((error) => {
			this.error = error.response.data.detail
		})
	}
};
</script>

<style scoped lang="scss">
	.supply{
		width: 100%;
		height: 100%;
	}
</style>