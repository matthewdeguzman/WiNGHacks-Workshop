<script lang="ts">
	import { v4 as uuidv4 } from 'uuid';
	import { beforeUpdate, afterUpdate } from 'svelte';
	import MessageElement from '$lib/components/message.svelte';
	import File from '$lib/components/file.svelte';
	import { type Message } from '$lib/message';
	import { type LLMResponse } from '$lib/llm-response';
	import { uploadedFile, selectedModel } from '$lib/stores';

	async function submitForm(event: Event) {
		console.log('submitting form...');
		event.preventDefault();
		messages = [...messages, { content: textArea.value, isUser: true, loading: false }];

		const formData: FormData = new FormData();
		console.log(textArea.value);
		console.log(fileUpload.files);
		formData.append('user_prompt', textArea.value);

		if (fileUpload.files && fileUpload.files.length > 0) {
			formData.append('file', fileUpload.files[0], fileUpload.files[0].name);
		}

		try {
			messages = [...messages, { content: '...', isUser: false, loading: true }];
			const response = await fetch('http://localhost:8000/prompt?llm='+$selectedModel, {
                method: 'POST',
				body: formData,
			});

            if (response.ok) {
                const result: LLMResponse = await response.json();
				messages[messages.length - 1].loading = false;
				messages[messages.length - 1].content = result.generated_text;
				messages = messages;
            } else {
				console.error('Server error:', await response.text());
                console.error('Server error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
	}

	function fileClick() {
		fileUpload.click();
	}

	function textInputHandler(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			submitButton.click();
			textArea.value = '';
		} else if (event.key == 'Enter' && event.shiftKey) {
			console.log("new line");
		}
	}

	function displayFile() {
		$uploadedFile = true;
	}

	beforeUpdate(() => {
		if (chat) {
			const scrollableDistance = chat.scrollHeight - chat.offsetHeight;
			autoscroll = chat.scrollTop > scrollableDistance - 20;
		}
	});

	afterUpdate(() => {
		if (autoscroll) {
			chat.scrollTo(0, chat.scrollHeight);
		}
	});	


	let fileUpload: HTMLInputElement;
	let textArea: HTMLTextAreaElement;
	let submitButton: HTMLButtonElement;
	let autoscroll: boolean = true;
	let chat: HTMLElement;
	let messages: Message[] = [];
	$: messages = messages;
</script>


<div class="page-container">
	<div class="message-container" class:empty-container={messages.length === 0} bind:this={chat}>
		{#if messages.length === 0}
			<img class="winghacks-logo" src={$selectedModel + ".gif"} alt={"image of " + $selectedModel} />
			<p class="blank-space">How can {$selectedModel} help you?</p>
		{/if}
		{#each messages as msg}
			<MessageElement message={msg} />
		{/each}
	</div>

	<div class="input-container">
		{#if $uploadedFile}
			<File filename={fileUpload.files[0].name} file={fileUpload}/>
		{/if}
		<div class="input-area">
			<form class="input-wrapper" class:display-file={$uploadedFile} on:submit|preventDefault={submitForm}>
				<div class="file">
					<button class="upload-btn" on:click|preventDefault={fileClick}>
						<img class="upload-img" src="/clip.svg" alt="attach files" />
					</button>
					<input bind:this={fileUpload} on:change={displayFile} type="file" accept=".pdf" class="hidden"/>
				</div>

				<textarea 
				on:keydown={textInputHandler}
				  placeholder="Message LLM..." autocorrect="off" autocomplete="off" data-gramm="false" data-gramm_editor="false" 
					data-enable-grammarly="false"
				 maxlength="1000"
				bind:this={textArea}
				/>

				<button on:click={submitForm} bind:this={submitButton} class="submit" type="submit">
					<img class="send" src="/enter.svg" alt="send message" />
				</button>
			</form>
		</div>
	</div>
</div>

<style>

	.input-area {
		width: 100%;
		grid-row: 2;
	}

	.input-wrapper {
		border: 1px solid black;
		border-radius: 5px;
		display: flex;
		flex-direction: row;
		align-items: center;
		height: 2.5rem;
	}

	.input-container {
		display: grid;
		grid-template-rows: repeat(2, 3rem);
		align-items: end;
		text-align: center;
		position: relative;
	}

	input[type="file"] {
		display: none;
	}

	textarea {
		resize: none;
		flex-grow: 1;
		outline: none !important;
		border: none;
		margin-right: 0.5rem;
		padding-top: 15px;
		background-color: transparent;
	}

	.hidden {
		display: none;
	}

	.send {
		width: 2rem;
		cursor: pointer;
	}

	.submit {
		border: none;
		background-color: transparent;
	}

	.upload-img {
		cursor: pointer;
		height: 1.5rem;
	}

	.upload-btn {
		border: none;
		background-color: transparent;
	}

	.message-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow-y: scroll;
		padding: 1.5rem;
	}

	.page-container {
		height: 80vh;
		display: grid;
		grid-template-rows: auto 3rem;
	}
	@media (max-height: 800px) {
		.page-container {
			height: 75vh;
			display: grid;
			grid-template-rows: auto 3rem;
		}
	}
	
	@media (max-height: 600px) {
		.page-container {
			height: 65vh;
			display: grid;
			grid-template-rows: auto 3rem;
		}
	}

	.empty-container {
		justify-content: center;
		align-items: center;
	}

	.winghacks-logo {
		width: 10rem;
		margin-bottom: 1rem;
	}

	.blank-space {
		font-weight: bold;
	}
</style>
