import unittest
import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.clock import SimulatedClock

class TestSmartVault(unittest.TestCase):

    def setUp(self):
        """Runs before every test. Sets up a fresh machine."""
        filepath = os.path.join(os.path.dirname(__file__), 'vault_complicated.yaml')
        self.statechart = import_from_yaml(filepath=filepath)
        self.clock = SimulatedClock()
        self.interpreter = Interpreter(self.statechart, clock=self.clock)
        self.interpreter.execute() # Boot the machine

    def assertInState(self, state_name):
        """Helper to check if the machine is currently in a specific state."""
        config = self.interpreter.configuration
        self.assertIn(state_name, config, f"Machine should be in '{state_name}' but is in {config}")

    def assertNotInState(self, state_name):
        config = self.interpreter.configuration
        self.assertNotIn(state_name, config, f"Machine should NOT be in '{state_name}'")

    def test_unlock_flow(self):
        """Test that correct PIN unlocks the door."""
        # Initial State
        self.assertInState('Locked')

        # Action
        self.interpreter.queue('PIN_ENTERED', code=1234).execute()

        # Assert
        self.assertInState('Unlocked')

    def test_wrong_pin_does_not_unlock(self):
        """Test that wrong PIN keeps door locked."""
        self.interpreter.queue('PIN_ENTERED', code=0000).execute()
        self.assertInState('Locked')
        self.assertNotInState('Unlocked')

    def test_auto_lock_timer(self):
        """Test that the door auto-locks after 2 seconds."""
        # 1. Unlock
        self.interpreter.queue('PIN_ENTERED', code=1234).execute()
        self.assertInState('Unlocked')

        # 2. Wait 1.9s (Should still be open)
        self.clock.time += 1.9
        self.interpreter.execute() # Force check
        self.assertInState('Unlocked')

        # 3. Wait 0.2s more (Total 2.1s) -> Should Lock
        self.clock.time += 0.2
        self.interpreter.execute() # Force check
        self.assertInState('Locked')

    def test_battery_drain_parallel(self):
        """Test that battery drains independently of the lock state."""
        self.assertInState('FullBattery')

        # Advance 4 seconds
        self.clock.time += 4.0
        self.interpreter.execute()

        self.assertInState('LowBattery')
        # Security region should still be active/locked
        self.assertInState('Locked')

    def test_master_reset_hierarchy(self):
        """Test that Master Reset works from ANY state."""
        # 1. Get into a deep state
        self.interpreter.queue('PIN_ENTERED', code=1234).execute()

        # Wait 4.0s. 
        # - Security: Unlocked -> Locked (at 2s via Auto-Lock)
        # - Power: Full -> Low (at 4s)
        self.clock.time += 4.0
        self.interpreter.execute()

        # FIX: Expect 'Locked' because auto-lock timer (2s) is shorter than battery timer (4s)
        self.assertInState('Locked')     
        self.assertInState('LowBattery')

        # 2. Hit the Kill Switch
        self.interpreter.queue('MASTER_RESET').execute()

        # 3. Assert we are in Maintenance and NOT in previous states
        self.assertInState('Maintenance')
        self.assertNotInState('Locked')
        self.assertNotInState('LowBattery')

if __name__ == '__main__':
    unittest.main()