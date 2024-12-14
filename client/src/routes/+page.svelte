<script>
	import { user } from '../stores/auth.js';
	import { onMount } from 'svelte';
	import Card from '../components/Card.svelte';

	let properties = [];

	let userDetails;
	$: userDetails = $user; // Reactive store subscription

	async function makeAuthorizedRequest() {
		if (!userDetails || !userDetails.token) {
			console.error('No token available. Please log in.');
			return;
		}

		try {
			const response = await fetch('http://localhost:8000/api/v1/spm/properties', {
				method: 'GET',
				headers: {
					'Authorization': `${userDetails.token}`, // Include token in the Authorization header
					'Content-Type': 'application/json',
				},
			});

			if (response.ok) {
				const data = await response.json();
				properties = data;
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

<div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
	{#each properties as property}
		<Card
			link={`/properties/${property.property_id_nma}`}
			address={property.property_id_nma}
			area={property.area}
			additionalInfo={`${property.number_of_sections} units in ${property.number_of_buildings} buildings`}
		/>
	{/each}
</div>

<style lang="postcss">
	:global(html) {
		background-color: theme(colors.gray.100);
	}
</style>
