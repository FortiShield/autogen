// Copyright (c) Microsoft Corporation. All rights reserved.
// IGateway.cs

namespace Microsoft.AutoGen.Abstractions;

public interface IGateway: IGrainObserver
{
    ValueTask<RpcResponse> InvokeRequest(RpcRequest request, CancellationToken cancellationToken = default);
    ValueTask BroadcastEvent(CloudEvent evt, CancellationToken cancellationToken = default);
    ValueTask StoreAsync(AgentState value, CancellationToken cancellationToken = default);
    ValueTask<AgentState> ReadAsync(AgentId agentId, CancellationToken cancellationToken = default);
    Task SendMessageAsync(IConnection connection, CloudEvent cloudEvent, CancellationToken cancellationToken = default);
}
