<script lang="ts">
	import { uploadedFile } from '$lib/stores';
	export let filename: string;
	export let file: HTMLInputElement;
	let displayClose: boolean = false;

	if (filename.length > 16) {
		filename = filename.slice(0, 16) + '...';
	}

	function closeFile() {
		file.value = '';
		$uploadedFile = false;
	}
</script>

<div class="file-container" on:mouseover={() => displayClose = true} on:mouseleave={() => displayClose = false}>
	<img class="file-img" src="/file.svg" alt="file icon" />
	<div class="file-information">
		<p class="file-name">{filename}</p>
		<p class="file-type">PDF</p>
	</div>
	<button class="delete-btn" class:hidden={!displayClose} on:click={closeFile}>
		<img class="delete-img " src="/close.svg" alt="delete file" />
	</button>
</div>

<style>
	.file-container {
		grid-row: 1;
		display: grid;
		grid-template-columns: 1rem auto;
		border: 1px solid black;
		border-radius: 5px;
		margin: 0.5rem 0;
		width: 10rem;
		padding: 0.3rem 0.2rem;
		position: relative;
	}

	.file-img {
		width: 1.7rem;
		height: 1.7rem;
		align-self: center;
	}

	.file-information {
		margin-left: 1rem;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}

	.file-type {
		font-size: 0.80rem;
	}

	.delete-btn {
		border: none;
		background-color: white;
		cursor: pointer;
		position: absolute;
		right: -0.9rem;
		top: -0.5rem;
	}

	.hidden {
		visibility: hidden;
	}

	.delete-img {
		width: 1rem;
	}

</style>
