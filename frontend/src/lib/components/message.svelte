<script lang="ts">
	import { type Message } from "$lib/message";
	import { selectedModel } from "$lib/stores";
	export let message: Message;
	const author: string = message.isUser ? "You" : $selectedModel;
	const avatar: string = author + ".gif";
</script>

<div class="message-wrapper">
	<img class="avatar" src={avatar} alt={author} />
	<h1 class="author">{author}</h1>
	{#if message.loading}
		<div class="loading">
			<img class="loading-img" src="/dot.svg" alt="loading" />
		</div>
	{:else}
		<p class="message">{message.content}</p>
	{/if}
</div>

<style>
	.message-wrapper {
		border-radius: 5px;
		height: fit-content;
		padding: 0.5rem;
		margin-bottom: 1rem;
		position: relative;
	}

	.author {
		font-weight: bold;
		margin-bottom: 0.5rem;
	}

	.message {
		line-height: 1.5;
	}

	.avatar {
		width: 1.5rem;
		height: 1.5rem;
		border-radius: 50%;
		position: absolute;
		top: 0.2rem;
		left: -1.3rem;
	}

	.loading-img {
		width: 1rem;
		animation: flash 1s infinite;
	}

	@keyframes flash {
		  0%, 100% { opacity: 1; }
		  50% { opacity: 0; }
	}

</style>
