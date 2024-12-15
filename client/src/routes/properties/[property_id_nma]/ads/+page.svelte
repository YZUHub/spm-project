<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { user } from '../../../../stores/auth.js';
    import ListingForm from '../../../../components/ListingForm.svelte';

    let userDetails;
	$: userDetails = $user; // Reactive store subscription

    async function handleFormSubmit(newListing) {
        try {
            const response = await fetch('http://localhost:8000/api/v1/ads', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `${userDetails.token}` },
                body: JSON.stringify(newListing)
            });

            if (response.ok) {
                const createdAd = await response.json(); // Assuming the response includes the created ad details
                console.log(createdAd);
                let url = `/listings/${createdAd.id}`;
                console.log(url);
                goto(url);
            } else {
                alert('Failed to create listing');
            }
        } catch (error) {
            console.error(error);
        }
    }
</script>

<ListingForm onSubmit={handleFormSubmit} listing={ { property_id_nma: $page.params.property_id_nma } } />
