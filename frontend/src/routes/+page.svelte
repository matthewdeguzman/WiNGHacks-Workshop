<script lang="ts">
	import MessageElement from '$lib/components/message.svelte';
	import { type Message } from '$lib/message';
	import { type LLMResponse } from '$lib/llm-response';

	async function submitForm(event: Event) {
		console.log('submitting form...');
		event.preventDefault();
		messages = [...messages, { content: textArea.value, isUser: true }];

		const formData: FormData = new FormData();
		console.log(textArea.value);
		console.log(fileUpload.files);
		formData.append('user_prompt', textArea.value);
		formData.append('file', fileUpload.files[0], fileUpload.files[0].name);

		try {
            // Send the form data to your server endpoint
            const response = await fetch('http://localhost:8000/prompt/', {
                method: 'POST',
				body: formData,
			});

            if (response.ok) {
                const result: LLMResponse = await response.json();
				messages = [...messages, { content: result.generated_text, isUser: false }];
                // Handle success (e.g., show a success message)
            } else {
				console.error('Server error:', await response.text());
                console.error('Server error:', response.statusText);
                // Handle server error (e.g., show an error message)
            }
        } catch (error) {
            console.error('Error:', error);
            // Handle network error (e.g., show an error message)
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

	let messages: Message[] = [];

	$: messages = messages;

	let fileUpload: HTMLInputElement;
	let textArea: HTMLTextAreaElement;
	let submitButton: HTMLButtonElement;
</script>


<div class="page-container">
	<div class="message-container">
		{#each messages as msg}
			<MessageElement message={msg} />
		{/each}
	</div>

	<div class="input-container">
		<form class="input-wrapper" on:submit|preventDefault={submitForm}>
			<div class="file">
				<button class="upload-btn" on:click|preventDefault={fileClick}>
					<img class="upload-img" src="/clip.svg" alt="attach files" />
				</button>
				<input bind:this={fileUpload} type="file" accept=".pdf" class="hidden"/>
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

<style>

	.input-wrapper {
		border: 1px solid black;
		border-radius: 5px;
		display: flex;
		flex-direction: row;
		align-items: center;
		width: 100%;
		height: 2.5rem;
	}

	.input-container {
		display: flex;
		flex-direction: row;
		align-items: end;
		text-align: center;
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
	}

	.page-container {
		height: 92vh;
		display: grid;
		grid-template-rows: auto 3rem;
	}
</style>
