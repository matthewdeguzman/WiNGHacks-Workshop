<script lang="ts">
	import { type Message } from "$lib/message";
	export let message: Message;
</script>

<div class="message-wrapper">
	<h1 class="author">{message.isUser ? 'You' : 'LLM'}</h1>
	<p class="message">{message.content}</p>
</div>

<style>
	.message-wrapper {
		border: 1px solid black;
		border-radius: 5px;
		height: fit-content;
		padding: 0.5rem;
		margin-bottom: 1rem;
	}

	.author {
		font-weight: bold;
		margin-bottom: 0.5rem;
	}
</style>
