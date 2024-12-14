<script>
	import { user } from '../stores/auth.js';
	import { onMount } from 'svelte';

	let userDetails;
	$: userDetails = $user; // Reactive store subscription

	async function makeAuthorizedRequest() {
		if (!userDetails || !userDetails.token) {
			console.error('No token available. Please log in.');
			return;
		}

		try {
			const response = await fetch('http://localhost:8000/api/v1/auth/validate', {
				method: 'GET',
				headers: {
					'Authorization': `${userDetails.token}`, // Include token in the Authorization header
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const data = await response.json();
				console.log('Response:', data);
			} else {
				console.error('Failed request:', response.status);
			}
		} catch (error) {
			console.error('Error making request:', error);
		}
	}

	onMount(() => {
		makeAuthorizedRequest();
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<h1 class="text-3xl font-bold underline">Hello world!</h1>

<style lang="postcss">
	:global(html) {
		background-color: theme(colors.gray.100);
	}
</style>
