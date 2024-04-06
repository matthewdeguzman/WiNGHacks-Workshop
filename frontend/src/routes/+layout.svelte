<script lang="ts">
	import Header from '$lib/components/header.svelte';
	import './reset.css';
	import './global.css';
</script>

<div class="container">
	<div class="content">
		<Header />
		<slot />
	</div>
</div>

<style>
	.container {
		display: grid;
		grid-template-columns: 100%;
		justify-items: center;
		padding: 0 1rem;
	}

	.content {
		width: 100%;
		max-width: 600px;
		height: 100vh;
		display: grid;
	}
</style>
