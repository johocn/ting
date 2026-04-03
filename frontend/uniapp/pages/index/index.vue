<template>
	<view class="content">
		<image class="logo" src="/static/logo.png"></image>
		<view class="text-area">
			<text class="title">{{ title }}</text>
		</view>
		<view class="features">
			<view class="feature-item">
				<text class="feature-title">学习中心</text>
				<text class="feature-desc">观看学习内容，参与答题</text>
			</view>
			<view class="feature-item">
				<text class="feature-title">积分商城</text>
				<text class="feature-desc">积分兑换礼品</text>
			</view>
			<view class="feature-item">
				<text class="feature-title">个人中心</text>
				<text class="feature-desc">个人信息管理</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Ting Learning Platform'
			}
		},
		onLoad() {

		},
		methods: {

		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}

	.features {
		width: 100%;
		padding: 20rpx;
		margin-top: 100rpx;
	}

	.feature-item {
		background-color: #f8f8f8;
		border-radius: 10rpx;
		padding: 20rpx;
		margin-bottom: 20rpx;
	}

	.feature-title {
		font-size: 32rpx;
		font-weight: bold;
		display: block;
	}

	.feature-desc {
		font-size: 28rpx;
		color: #8f8f94;
		display: block;
		margin-top: 10rpx;
	}
</style>