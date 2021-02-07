<template>
	<div class="input-overlay" v-if="isSearching">
		<qrcode-stream v-on:decode="onDecode" v-bind:track="checkQR" v-bind:camera="cameraMode" v-on:init="onInit"></qrcode-stream>
		<form @submit.prevent="searchByNumber(number)">
			<p class="search-number">
				<label for="search-number" style="display: none">番号で検索</label>
				<input type="text" id="search-number" v-model="number" placeholder="番号で検索">
				<input type="submit" value="検索">
			</p>
		</form>
		<div class="close" v-if="canClose" v-on:click="$emit('close')">×</div>
		<p class="error">{{ error }}</p>
	</div>
</template>

<script>
import SupplySearchResultList from "@/components/SupplySearchResultList";
import {QrcodeStream} from "vue-qrcode-reader";

export default {
	name: "SupplySearch",
	props: {
		isSearching: {
			type: Boolean,
			default: true,
		},
		canClose: {
			type: Boolean,
			default: true
		},
		supplyRejectList: {
			type: Array,
			default() {
				return []
			}
		},
		value: String,
	},
	data() {
		return {
			result: "",
			error: "",
			number: "",
		}
	},
	components: {
		QrcodeStream,
	},
	computed: {
		cameraMode() {
			return this.isSearching ? "auto" : "off"
		},
		localValue: {
			get() {
				return this.value
			},
			set(value) {
				this.$emit("input", value)
			}
		}
	},
	methods: {
		searchByNumber(number) {
			this.$api.get(`supply/search/${number}`)
				.then((response) => {
					if (response.data.length === 1){
						this.localValue = response.data[0].uuid
					} else if (response.data.length > 1) {
						this.$modal.show(
							SupplySearchResultList,
							{
								supplies: response.data,
								value: this.test,
								message: "複数の結果が見つかりました。下から選んでください。"
							},
							{
								width: 800,
								resizable: true,
							},
							{
								"before-close": event => {
									if (event.params.match(/([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})/)){
										this.localValue = event.params
									}
								}
							}
						)
					}
				})
				.catch(() => {
					this.printMessage(location, ctx, "Error!: 登録されていない備品です。")
					return
				})
		},
		onDecode(result) {
			this.result = result
		},
		checkQR(location, ctx) {
			const hostname = process.env.VUE_APP_QR_HOSTNAME
			const regExp = new RegExp(hostname.replaceAll("\.", "\\.") + "\/([0-9a-f]{8})([0-9a-f]{4})([0-9a-f]{4})([0-9a-f]{4})([0-9a-f]{12})")
			const match = this.result.match(regExp)
			if (!match) {
				this.printMessage(location, ctx, "他のQRコードです。")
				return;
			}
			const uuid = `${match[1]}-${match[2]}-${match[3]}-${match[4]}-${match[5]}`
			if (this.supplyRejectList.includes(uuid)) {
				this.printMessage(location, ctx, "既に追加済みです。")
				return
			}
			this.$api.get(`supply/${uuid}`)
				.then((response) => {
					this.localValue = response.data.uuid
				})
				.catch(() => {
					this.printMessage(location, ctx, "Error!: 登録されていない備品です。")
					return
				})
		},
		printMessage(location, ctx, message) {
			const {
				topLeftCorner,
				topRightCorner,
				bottomLeftCorner,
				bottomRightCorner
			} = location

			const pointArray = [
				topLeftCorner,
				topRightCorner,
				bottomLeftCorner,
				bottomRightCorner
			]

			const centerX = pointArray.reduce((sum, {x}) => x + sum, 0) / 4
			const centerY = pointArray.reduce((sum, {y}) => y + sum, 0) / 4

			ctx.font = "bold 24px sans-serif"
			ctx.textAlign = "center"

			ctx.lineWidth = 5
			ctx.strokeStyle = '#ffffff'
			ctx.strokeText(message, centerX, centerY)

			ctx.fillStyle = '#ff0000'
			ctx.fillText(message, centerX, centerY)
		},
		async onInit (promise) {
			try {
				await promise
			} catch (error) {
				if (error.name === 'NotAllowedError') {
					this.error = "ERROR: カメラへのアクセスを許可してください"
				} else if (error.name === 'NotFoundError') {
					this.error = "ERROR: カメラがありません"
				} else if (error.name === 'NotSupportedError') {
					this.error = "ERROR: secure context required (HTTPS, localhost)"
				} else if (error.name === 'NotReadableError') {
					this.error = "ERROR: is the camera already in use?"
				} else if (error.name === 'OverconstrainedError') {
					this.error = "ERROR: installed cameras are not suitable"
				} else if (error.name === 'StreamApiNotSupportedError') {
					this.error = "ERROR: Stream API is not supported in this browser"
				}
			}
		}
	}
};
</script>

<style lang="scss" scoped>

.input-overlay{
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	z-index: 98;
	background-color: rgba(#000000, 0.8);
	.close{
		font-size: 32px;
		position: fixed;
		top: 0;
		right: 0;
		width: 40px;
		height: 40px;
		color: white;
		cursor: pointer;
		z-index: 100;
	}
	.error{
		font-size: 24px;
		color: red;
		position: fixed;
		top: 50%;
		left: 50%;
		z-index: 99;
		transform: translate(-50%, -50%);
	}
	.search-number{
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 32px;
		color: white;
		position: fixed;
		bottom: 0;
		left: 50%;
		transform: translateX(-50%);
		z-index: 100;
		input{
			font-size: 32px;
			padding: 5px;
		}
	}
}
</style>