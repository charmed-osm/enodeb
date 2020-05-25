#!/usr/bin/env python3

import sys

sys.path.append("lib")

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import (
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus,
    WaitingStatus,
    ModelError,
)
import subprocess


class EnodebCharm(CharmBase):
    state = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        # An example of setting charm state
        # that's persistent across events
        self.state.set_default(is_started=False)

        if not self.state.is_started:
            self.state.is_started = True

        # Register all of the events we want to observe
        for event in (
            # Charm events
            self.on.config_changed,
            self.on.install,
            self.on.upgrade_charm,
            self.on.register_action,
        ):
            self.framework.observe(event, self)

    def on_config_changed(self, event):
        """Handle changes in configuration"""
        unit = self.model.unit

    def on_install(self, event):
        """Called when the charm is being installed"""
        unit = self.model.unit

        # Install your software and its dependencies

        unit.status = ActiveStatus()

    def on_upgrade_charm(self, event):
        """Upgrade the charm."""
        unit = self.model.unit

        # Mark the unit as under Maintenance.
        unit.status = MaintenanceStatus("Upgrading charm")

        self.on_install(event)

        # When maintenance is done, return to an Active state
        unit.status = ActiveStatus()

    def on_register_action(self, event):
        """Register to AGW (EPC)."""
        try:
            mme_addr = event.params["mme-addr"]
            gtp_bind_addr = event.params["gtp-bind-addr"]
            s1c_bind_addr = event.params["s1c-bind-addr"]
            command = " ".join(
                [
                    "srsenb",
                    "--enb.name=dummyENB01",
                    "--enb.mcc=901",
                    "--enb.mnc=70",
                    "--enb.mme_addr={}".format(mme_addr),
                    "--enb.gtp_bind_addr={}".format(gtp_bind_addr),
                    "--enb.s1c_bind_addr={}".format(s1c_bind_addr),
                    "--enb_files.rr_config=/config/rr.conf",
                    "--enb_files.sib_config=/config/sib.conf",
                    "--enb_files.drb_config=/config/drb.conf",
                    "/config/enb.conf.fauxrf",
                ]
            )
            stdout = subprocess.check_output(command, shell=True)
            event.set_results({"output": stdout})
        except subprocess.CalledProcessError as ex:
            event.fail(ex)


if __name__ == "__main__":
    main(EnodebCharm)
