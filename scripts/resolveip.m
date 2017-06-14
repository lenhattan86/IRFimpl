function [ipaddress, hostname] = resolveip(input)

try 
	address = java.net.InetAddress.getByName(input);
catch 
	error(sprintf('Unknown host %s.', input))
end
hostname = char(address.getHostName);
ipaddress = char(address.getHostAddress);
end