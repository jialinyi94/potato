import jax
import optax
from pyfoliopt.optimizer import proj_gd

import jax.numpy as jnp


def test_proj_gd():
    # Define a simple learning rate schedule
    lr_schedule = 0.1

    # Define a simple projection function (e.g., clipping to [0, 1])
    def projection_fn(x):
        return jnp.clip(x, 0, 1)

    # Initialize the optimizer
    optimizer = proj_gd(lr_schedule, projection_fn)
    params = jnp.array([0.5, 1.5, -0.5])
    state = optimizer.init(params)

    # Define some dummy gradients
    updates = jnp.array([0.1, -0.2, 0.3])

    # Perform an update step
    transformed_updates, new_state = optimizer.update(updates, state, params)

    # Check the new state
    assert new_state.count == 1

    # Check the transformed updates
    expected_params = params - lr_schedule * updates
    expected_params_proj = jnp.clip(expected_params, 0, 1)
    expected_transformed_updates = expected_params_proj - expected_params

    assert jnp.allclose(transformed_updates, expected_transformed_updates)
