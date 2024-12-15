<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    const id = $page.params.id;

    let adDetails = null;
    let loading = true;

    // Fetch the ad details from the backend using the ID from the route
    async function fetchAdDetails(id) {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/ads/${id}`);
            if (response.ok) {
                adDetails = await response.json();
            } else {
                console.log('Failed to fetch ad details');
            }
        } catch (err) {
            console.log('Error fetching ad details');
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        fetchAdDetails(id);
    });
</script>

{#if loading}
	<div class="flex justify-center items-center min-h-screen">
		<div class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-[var(--color-bg-2)] border-t-[var(--color-accent)]"></div>
	</div>
{:else if adDetails}
<!-- Property Details -->
    <div class="p-8 space-y-6">
        <!-- Property Image -->
        <div class="relative w-full h-96 rounded-lg overflow-hidden shadow-md">
            <img
                src="/property-placeholder.jpg"
                alt="Property"
                class="w-full h-full object-cover"
            />
            <div class="absolute bottom-0 left-0 bg-gradient-to-t from-black/90 to-40 w-full p-4 pt-96 text-white">
                <h1 class="text-2xl font-bold">📍{adDetails.address}</h1>
                <p class="text-lg">🔗{adDetails.property_id_nma} • NOK {adDetails.price.toLocaleString()}</p>
            </div>
        </div>

        <!-- Title, Type, Status, Price, and Link -->
        <div class="space-y-4">
            <h1 class="text-3xl font-bold">{adDetails.title}</h1>
            <p class="text-sm text-gray-400">Type: {adDetails.type} | Status: {adDetails.status}</p>
            <p class="text-lg font-semibold">Price: NOK {adDetails.price.toLocaleString()}</p>
            <a 
                href={`/properties/${adDetails.property_id_nma}`} 
                class="text-blue-400 hover:underline"
            >
                View Property Details →
            </a>
        </div>

        <!-- Description -->
        <div class="description mt-4 text-gray-200 text-justify">
            {#each adDetails.description.split('\n') as paragraph}
                <p class="mb-4">{paragraph}</p>
            {/each}
        </div>

        <!-- Listed By -->
        <div class="space-y-2">
            <h2 class="text-lg font-semibold">Posted By</h2>
            <p class="text-gray-400">{adDetails.listed_by}</p>
        </div>
    </div>
{:else}
    <div class="flex justify-center items-center min-h-screen">
        <p class="text-xl text-[var(--color-text-muted)]">No listing details found</p>
    </div>
{/if}

<style>
    :global(body) {
        background-color: #1a202c; /* Dark gray background for the page */
    }
</style>
