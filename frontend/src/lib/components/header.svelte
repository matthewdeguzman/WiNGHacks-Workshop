<script lang="ts">
	import { selectedModel } from '$lib/stores';
	let selectElement: HTMLSelectElement;

	function updateSelection() {
		$selectedModel = selectElement.value;
	}
</script>

<select name="llm" id="llm" class="llm-select" bind:this={selectElement} on:change={updateSelection}>
	<option value="Mushwoom">Mushwoom</option>
	<option value="William">William</option>
</select>

<style>
	.llm-select{
		width: fit-content;
		margin-top: 1rem;
		justify-self: begin;
		font-size: 1rem;
		font-weight: bold;
		height: 2rem;
		border: none;
	}

	.llm-select:focus{
		outline: none;
	}
</style>
