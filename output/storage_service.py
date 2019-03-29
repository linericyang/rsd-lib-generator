from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

# from  import remote_targets
# from  import logical_drives
# from  import drives


class LinksField(base.CompositeField):

    managed_by = base.Field("ManagedBy", adapter=utils.get_members_identities)


class StorageService(rsd_lib_base.ResourceBase):

    status = rsd_lib_base.StatusField("Status")
    """This indicates the known state of the resource, such as if it is
       enabled.
    """

    links = LinksField("Links")

    @property
    @utils.cache_it
    def remote_targets(self):
        """Property to provide reference to `RemoteTargetCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return remote_target.RemoteTargetCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "RemoteTargets"),
            redfish_version=self.redfish_version,
        )

    @property
    @utils.cache_it
    def logical_drives(self):
        """Property to provide reference to `LogicalDriveCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return logical_drive.LogicalDriveCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "LogicalDrives"),
            redfish_version=self.redfish_version,
        )

    @property
    @utils.cache_it
    def drives(self):
        """Property to provide reference to `PhysicalDriveCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return physical_drive.PhysicalDriveCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Drives"),
            redfish_version=self.redfish_version,
        )


class StorageServiceCollection(rsd_lib_base.ResourceCollectionBase):
    @property
    def _resource_type(self):
        return StorageService
