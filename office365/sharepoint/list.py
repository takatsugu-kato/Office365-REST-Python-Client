from office365.runtime.client_query import ClientQuery, UpdateEntityQuery, DeleteEntityQuery, ServiceOperationQuery
from office365.runtime.odata.odata_path_parser import ODataPathParser
from office365.runtime.resource_path_entity import ResourcePathEntity
from office365.runtime.resource_path_service_operation import ResourcePathServiceOperation
from office365.runtime.utilities.http_method import HttpMethod
from office365.sharepoint.content_type_collection import ContentTypeCollection
from office365.sharepoint.field_collection import FieldCollection
from office365.sharepoint.folder import Folder
from office365.sharepoint.listitem import ListItem
from office365.sharepoint.listItem_collection import ListItemCollection
from office365.sharepoint.securable_object import SecurableObject
from office365.sharepoint.view import View
from office365.sharepoint.view_collection import ViewCollection


class List(SecurableObject):
    """List client object"""

    def get_items(self, caml_query=None):
        """Returns a collection of items from the list based on the specified query."""
        items = ListItemCollection(self.context, ResourcePathEntity(self.context, self.resourcePath, "items"))
        if caml_query:
            qry = ServiceOperationQuery(self, HttpMethod.Post, "GetItems", None, caml_query)
            self.context.add_query(qry, items)
        return items

    def add_item(self, list_item_creation_information):
        """The recommended way to add a list item is to send a POST request to the ListItemCollection resource endpoint,
         as shown in ListItemCollection request examples."""
        item = ListItem(self.context, None, list_item_creation_information)
        item._parent_collection = self
        qry = ClientQuery(self.resourceUrl + "/items", HttpMethod.Post, item)
        self.context.add_query(qry, item)
        return item

    def get_item_by_id(self, item_id):
        """Returns the list item with the specified list item identifier."""
        return ListItem(self.context,
                        ResourcePathServiceOperation(self.context, self.resourcePath, "getitembyid", [item_id]))

    def get_view(self, view_id):
        """Returns the list view with the specified view identifier."""
        view = View(self.context, ResourcePathServiceOperation(self.context,
                                                               self.resourcePath,
                                                               "getview",
                                                               [view_id]))
        return view

    def update(self):
        qry = UpdateEntityQuery(self)
        self.context.add_query(qry)

    def delete_object(self):
        """Deletes the list."""
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)
        # self.removeFromParentCollection()

    @property
    def rootFolder(self):
        """Get a root folder"""
        if self.is_property_available('RootFolder'):
            return self.properties["RootFolder"]
        else:
            return Folder(self.context, ResourcePathEntity(self.context, self.resourcePath, "RootFolder"))

    @property
    def fields(self):
        """Gets a value that specifies the collection of all fields in the list."""
        if self.is_property_available('Fields'):
            return self.properties['Fields']
        else:
            return FieldCollection(self.context, ResourcePathEntity(self.context, self.resourcePath, "Fields"))

    @property
    def views(self):
        """Gets a value that specifies the collection of all public views on the list and personal views
        of the current user on the list."""
        if self.is_property_available('Views'):
            return self.properties['Views']
        else:
            return ViewCollection(self.context, ResourcePathEntity(self.context, self.resourcePath, "views"))

    @property
    def contentTypes(self):
        """Gets the content types that are associated with the list."""
        if self.is_property_available('ContentTypes'):
            return self.properties['ContentTypes']
        else:
            return ContentTypeCollection(self.context,
                                         ResourcePathEntity(self.context, self.resourcePath, "contenttypes"))

    def set_property(self, name, value, serializable=True):
        super(List, self).set_property(name, value, serializable)
        # fallback: create a new resource path
        if self._resource_path is None:
            if name == "Id":
                self._resource_path = ResourcePathEntity(
                    self.context,
                    self._parent_collection.resourcePath,
                    ODataPathParser.from_method("GetById", [value]))
            elif name == "Title":
                self._resource_path = ResourcePathEntity(
                    self.context,
                    self._parent_collection.resourcePath,
                    ODataPathParser.from_method("GetByTitle", [value]))


