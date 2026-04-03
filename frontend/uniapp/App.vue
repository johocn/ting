<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/* uni.css - 通用组件、模板样式库，可以当作一套ui库使用 */
	@import './static/uni.css';
	
	/* 自定义全局样式 */
	view, text, scroll-view {
		box-sizing: border-box;
	}
</style>